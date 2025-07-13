package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Developer;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IDeveloperService {
    Developer add(String name);
    List<Developer> findAll();
    Developer findById(Integer id);
    Developer findByName(String name);
    boolean delete(Integer id);
    Developer update(Integer id, String name);
}
