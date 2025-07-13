package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.Platform;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IPlatformService {
    Platform add(String name);
    List<Platform> findAll();
    Platform findById(Integer id);
    Platform findByName(String name);
    boolean delete(Integer id);
    Platform update(Integer id, String name);
}
