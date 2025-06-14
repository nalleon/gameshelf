package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Developer;

import java.util.List;

public interface IDeveloperRepository {
    Developer save(Developer developer);
    List<Developer> findAll();
    Developer findById(Integer id);
    Developer findByName(String name);
    boolean delete(Integer id);
    Developer update(Developer developer);
}
